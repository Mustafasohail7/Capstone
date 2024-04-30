import sys
import cv2
import os

from rivamap import singularity_index, delineate, preprocess, visualization
from test_rasterio import *

def main(process_all):
    current_directory = os.getcwd()
    download_directory = os.path.join(current_directory, "downloads")

    download_files = os.listdir(download_directory)
    for index,item in enumerate(download_files):
        if process_all or index==0:
            file_directory = os.path.join(download_directory, item)
            if os.path.isdir(file_directory):
                tif_files = os.listdir(file_directory)
                found = [False, False]
                b3_path = None
                for tif_file in tif_files:
                    if tif_file.endswith('.TIF'):
                        if 'B3' in tif_file:
                            tif_file_path = os.path.join(file_directory, tif_file)
                            B3 = cv2.imread(tif_file_path, cv2.IMREAD_UNCHANGED)
                            b3_path = tif_file_path
                            found[0] = True
                        elif 'B6' in tif_file:
                            tif_file_path = os.path.join(file_directory, tif_file)
                            B6 = cv2.imread(tif_file_path, cv2.IMREAD_UNCHANGED)
                            found[1] = True
                        else:
                            continue
                    if found[0] and found[1]:
                        process_image(B3, B6, b3_path)
                        break
                if not found[0] or not found[1]:
                    print("Could not find B3 and B6 files in directory:", file_directory)
                    return

def process_image(B3,B6,tif_file_b3):
    # Compute the modified normalized difference water index of the input
    I1 = preprocess.mndwi(B3, B6)

    # Create the filters that are needed to compute the singularity index
    filters = singularity_index.SingularityIndexFilters()

    # Compute the modified multiscale singularity index
    psi, widthMap, orient = singularity_index.applyMMSI(I1, filters)

    # Extract channel centerlines
    nms = delineate.extractCenterlines(orient, psi)
    centerlines = delineate.thresholdCenterlines(nms)

    print(centerlines)

    # Generate a raster map of the extracted channels
    raster = visualization.generateRasterMap(centerlines, orient, widthMap)

    print("generating vector map")

    current_directory = os.getcwd()
    output_directory = os.path.join(current_directory, "output")
    os.makedirs(output_directory, exist_ok=True)

    # Generate a vector map of the extracted channels
    visualization.generateVectorMap(centerlines, orient, widthMap, saveDest = "output/vector.pdf")

    print("generating quiver plot")

    # Generate a quiver plot
    visualization.quiverPlot(psi, orient, saveDest = "output/quiver.pdf")

    print("saving images now")

    # Save the images that are created at the intermediate steps
    cv2.imwrite("output/mndwi.TIF", cv2.normalize(I1, None, 0, 255, cv2.NORM_MINMAX))
    cv2.imwrite("output/psi.TIF", cv2.normalize(psi, None, 0, 255, cv2.NORM_MINMAX))
    cv2.imwrite("output/nms.TIF", cv2.normalize(nms, None, 0, 255, cv2.NORM_MINMAX))
    cv2.imwrite("output/centerlines.TIF", centerlines.astype(int)*255)
    cv2.imwrite("output/rasterMap.TIF", cv2.normalize(raster, None, 0, 255, cv2.NORM_MINMAX))

    gm = loadGeoMetadata(tif_file_b3)
    saveAsGeoTiff(gm, raster, "output/raster_geotagged.TIF")
    exportCSVfile(centerlines, widthMap, gm, "output/results.csv")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python main.py [<start_date>] [<end_date>] [<file_path>] [<bands>]")
        sys.exit(1)

    process_all = '-all' in sys.argv

    main(process_all)
