def mndwi(green, mir):
    """ Computes the modified normalized difference water index
    
    Inputs:
    green -- green band (e.g. Landsat 8 band 3)
    mir -- middle infrared band (e.g. Landsat 8 band 6)
    
    Returns:
    mndwi -- mndwi response
    """
    
    green = im2double(green)
    mir = im2double(mir)
        
    numerator = green+mir
    denominator = green-mir
    numerator[denominator==0] = 0
    denominator[denominator==0] = 1
    mndwi = numerator / denominator
        
    return mndwi

def im2double(I):
    """ Converts image datatype to float """
    if I.dtype == 'uint8':
        I = I.astype('float')/255
        
    if I.dtype == 'uint16':
        I = I.astype('float')/65535
    
    return I