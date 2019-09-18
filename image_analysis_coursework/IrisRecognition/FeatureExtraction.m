function [feature_array]=FeatureExtraction(enhanceI)
ROI=enhanceI((1:48),:);
channel1_deltax=3;
channel1_deltay=1.5;
channel2_deltax=4.5;
channel2_deltay=1.5;
f1=1/channel1_deltay;
f2=1/channel2_deltay;
channel1_matrix=gabor_matrix(9,channel1_deltax,channel1_deltay,f1);
channel2_matrix=gabor_matrix(9,channel2_deltax,channel2_deltay,f2);



filter1=conv2(ROI,channel1_matrix,'same');
filter2=conv2(ROI,channel2_matrix,'same');

array1=double([]);
for i=1:6
    for j=1:64
        submatrix=filter1((8*i-7):8*i,(8*j-7):8*j);
        [nrow,ncol]=size(submatrix);
        subarray=reshape(submatrix,1,nrow*ncol);
        array1=cat(2,array1,subarray);
    end
end

array2=double([]);
for i=1:6
    for j=1:64
        submatrix=filter2((8*i-7):8*i,(8*j-7):8*j);
        [nrow,ncol]=size(submatrix);
        subarray=reshape(submatrix,1,nrow*ncol);
        array2=cat(2,array2,subarray);
    end
end

feature_array1=double([]);
for i=1:384
    mean_region=mean(array1((64*i-63):64*i));
    abs_var=mean(abs(array1((64*i-63):64*i)-mean_region));
    feature_array1=cat(2,feature_array1,mean_region);
    feature_array1=cat(2,feature_array1,abs_var);
end

feature_array2=double([]);
for i=1:384
    mean_region=mean(array2((64*i-63):64*i));
    abs_var=mean(abs(array2((64*i-63):64*i)-mean_region));
    feature_array2=cat(2,feature_array2,mean_region);
    feature_array2=cat(2,feature_array2,abs_var);
end

feature_array=cat(2,feature_array1,feature_array2);
end