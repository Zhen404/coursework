clear;
load('train.mat');
load('test.mat');
[nrow1,ncol1]=size(train);
[nrow2,ncol2]=size(test);
h = waitbar(0,'Please wait...');
steps = ncol1+ncol2;
step=0;
for i=1:ncol1
    I=reshape(train(:,i),280,320);
    [pupil_center,pupil_radius,iris_radius]=IrisLocalization(I);
    for m=1:7
        normI=IrisNormalization(I,pupil_center,pupil_radius,iris_radius,-9+3*(m-1));
        enhanceI=ImageEnhancement(normI);
        train_feature(7*(i-1)+m,:)=FeatureExtraction(enhanceI);
    end 
    step=step+1;
    waitbar(step / steps)
end




for i=1:ncol2
    I=reshape(test(:,i),280,320);
    [pupil_center,pupil_radius,iris_radius]=IrisLocalization(I);
    normI=IrisNormalization(I,pupil_center,pupil_radius,iris_radius,0);
    enhanceI=ImageEnhancement(normI);
    test_feature(i,:)=FeatureExtraction(enhanceI); 
    step=step+1;
    waitbar(step / steps)
end
close(h)

save train_feature.mat train_feature;
save test_feature.mat test_feature;


