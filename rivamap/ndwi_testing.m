B3 = im2double(imread('band_3.TIF'));
B5 = im2double(imread('band_5.TIF'));
B6 = im2double(imread('band_6.TIF'));

imshow(B3);
%%
ndwi_num = B3-B5;
ndwi_den = B3+B5;
ndwi_fake = ndwi_den./ndwi_num;
I = imread('mndwi.TIF');
bruh = imabsdiff(ndwi_fake, I);
imshow(bruh)
ndwi = ndwi_num./(ndwi_den);
imshow(ndwi_fake);
%%
mndwi_num = B3-B6;
mndwi_den = B3+B6;

mndwi = mndwi_num./mndwi_den;

imshow(mndwi);
%%
%imshow(B3);imshow(B6);
I = imread("mndwi.TIF");
imshow(~I);
%%
I_log = mat2gray(2*log(1+I));
imshow(I_log);