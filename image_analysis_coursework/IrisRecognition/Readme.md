
The implementation of Iris Recognition follows Li Ma's Method

# Workflow

1. Load train and test iris data of 108 people (*Loaddata.m*)
2. Iris Localization -- Find pupil and iris (*IrisLocalization.m*)
3. Iris Normalization -- Convert iris region into a rectangular region (*IrisNormalization.m*,*Interpolate.m*)
4. Image Enhancement -- Eliminate the effect of the illunimation and equalize histogram based on $32\times32$ region (*ImageEnhancement.m*)
5. Feature Extraction --Use two gabor filter channels to get two outputs, calculate mean and absolute variance of $8\times8$ region among the whole image and save them as feature tables (*FeatureExtraction.m*, *gabor_channel.m*, *gabor_matrix.m*)
6. Iris Matching -- Use center nearest method to assign class for test data based on original feature table and reduced feature table (PCA+LDA) (*IrisMatching.m*, *PCAReduction.m*, *LDAReduction.m*)
7. PerformanceEvaluation --Output CRR (Correct Recognition Rate) under different similarity measure and graph showing CRR with respect to dimensionality of the feature vector (*PerformanceEvaluation.m*, *CrrTable.m*, *CRRdim.m*)

## Loaddata.m

Here we use for loop to change file path and save each image as a $1\times(280\times320)$ vector. Then we get train matrix and test matrix. I save them as **train.mat** and **test.mat** for further use.

## IrisLocalization.m

Input: I<br/>
Output: pupil_radius, pupil_center, iris_radius

```
blur=imgaussfilt(I,5);
```
First we use gaussian filter to eliminate the effect of eyelashes.

```
bw=imbinarize(blur,0.3);
sumx=sum(bw,1);
sumy=sum(bw,2);

[v1,ind_x]=min(sumx);
[v2,ind_y]=min(sumy);

estimate_center=[ind_x,ind_y];
estimate_radius=(320-v1+280-v2)/4;
```
Set a threshold 0.3 to get the binary image and locate the esitimate pupil center and pupil radius.

```
bw2=edge(blur,'canny');
bw2=bwareaopen(bw2,40);
```

Get the edge image and eliminate the connections less than 40 pixels (the effect of small connection within iris area)

```
[pupil_centers,pupil_radii]=imfindcircles(bw2,[floor(0.8*estimate_radius),floor(1.8*estimate_radius)],...
    'ObjectPolarity','dark','Method','TwoStage','Sensitivity',0.91,'EdgeThreshold',0.1);
```


Use *imfindcircles* function to find pupil. Radius range is 0.8~1.8 times of esitimate radius, which will give us a good circle for pupil. Sensitivity means how round of the circle we will regard it as a circle. EdgeThreshold means how complete of the curve to help us find the circle. We set a small number 0.1 because we want to use a small part of a circle to detect the wholes circle. 

This function may result multiple circles. We will choose the one which is closed to the estimate pupil center.

```
[iris_centers,iris_radii]=imfindcircles(bw2,[90,110],...
    'ObjectPolarity','dark','Method','TwoStage','Sensitivity',0.99,'EdgeThreshold',0.1);
```
In the similar way, we set radius range as 90~110, which I test could fit almost good for all images. The sensitivity is larger because we require a more round circle in edge image as an iris bound. We also choose the one which is closed to the estimate pupil center based on multiple circles we find.

Here I check all images. I choose regard the iris and pupil share the same center which gives a better result rather than regard the centers are different. This why we only output the pupil center.

## IrisNormalization.m

Input: I, pupil_center, pupil_radius, iris_radius, rotation<br/>
Output: NormI

This part strictly follows Li Ma's Method. As I mentioned in previous part, I regard that pupil and iris share the same center. Due to the localization problem, sometimes the annular ring we find may not contained totally in the image. Thus I use the following code to keep our normalization smoothly. But this way may cause some error while matching.

```
        if ceil(x)>320 || ceil(y)>280 || floor(x)<=0 || floor(y)<=0
            continue
             
        else
            normI(Y,X)=interpolate(I,y,x);
        end

```

I include rotation angle as a paramenter for further use. Modify the algorithm as follow,
```
theta=2*pi*(X+rotation)/N;
```

#### interpolate.m

In *IrisNormalization* function, I called the *interpolate* function. I refer https://github.com/sharadmv/iris-recognition/blob/master/matlab/ImToPolar.m to realize interpolation. Although matlab has buildin function of interpolation. I try to practice writing the interpolation explicitly.

## ImageEnhancement.m

Input: NormI<br/>
Output: enhanceI

Based on Li Ma's method, we first use mean filter over $16\times16$ region among the whole image to get the illumination of the how picture

```
h = 1/16*ones(16,1);
H = h*h';
imfilt = filter2(H,normI);
```

Then we subtruct the whole image by the filtered image to eliminate the effect of the illumination.
```
subtractI=normI-imfilt;
```

Finally do histogram equalization over $32\times32$ region among the whole image to increase the contrast of the normalized image. 2 is the the number of rows after blocking. 16 is the number of column after blocking.

```
enhanceI=adapthisteq(subtractI,'NumTiles',[2,16]);
```

## FeatureExtraction.m

Input: enhanceI<br/>
Output: feature_array

We first crop the enhanced image to $48\times512$ size.
```
ROI=enhanceI((1:48),:)
```
Then get two filter matrix.
```
channel1_deltax=3;
channel1_deltay=1.5;
channel2_deltax=4.5;
channel2_deltay=1.5;
f1=1/channel1_deltay;
f2=1/channel2_deltay;
channel1_matrix=gabor_matrix(9,channel1_deltax,channel1_deltay,f1);
channel2_matrix=gabor_matrix(9,channel2_deltax,channel2_deltay,f2);
```
Do convolution using two filter matrix and get two output matrix.
```
filter1=conv2(ROI,channel1_matrix,'same');
filter2=conv2(ROI,channel2_matrix,'same');
```

Use for loop to reorgnize the matrix information according to $8\times8$ region among matrix as a vector. Then use another for loop extract mean and absolute variance of every 64 elements of the vector and save them in a feature vector in sequence. Do the same procedure over both two channel output matrix. And finally get 1535 dimension vector as our final output *feature_array*.



#### gabor_channel.m

This is actually a modified gabor filter. We code it as the paper describes.

#### gabor_matrix.m

This is the function to get a filter matrix according to the function we define in *gabor_channel*, given symmetric range of x and y.



## Main.m

Combine the functions together and get the train feature table and test table. For each image of train set, we do localization, normalization over 7 rotation angle(-9, -6, -3, 0, 3, 6, 9), image enhancement and feature extraction. For each image of test set, we do the same procedure except normalization. We do normalization over rotation angle 0 only for test set. After waiting a couple of minutes, we finish preparing our ($2268\times1536$) *train_feature* table and ($432\times1536$) *test_feature* table. And I save them as *train_feature.mat* and *test_feature.mat* for further use.

## IrisMatching.m

Input: train_feature, test_feature, train_class<br/>
Output: predict_class1,predict_class2,predict_class3

Use center nearest method to assign class to test data under three distance measure:<br/>
L1 distance
```
dist1(i,j)=sum(abs(train_feature(j,:)-test_feature(i,:)))
```
L2 distance
```
dist2(i,j)=sqrt(sum((train_feature(j,:)-test_feature(i,:)).^2));
```
L3 distance
```
dist3(i,j)=1-train_feature(j,:)*test_feature(i,:)'/(norm(train_feature(j,:))*norm(test_feature(i,:)));
```

Pairwisely calculate those distances between train and test. And assign train data class corresponding the cloest distance to test data.<br/>

We will also consider dimension reduction here. The method I used here is doing PCA to reduce the dimension to 495 first (I tried a lot dimensions, 495 can perform a relatively good result) and then use LDA to reduce the dimension to contain 99 percent of the variance of train data.

#### PCAReduction.m

First center data and mainly use *pca* function. 
```
[coeff,score,latent]=pca(center_train_feature);
dim_pca=495;

projection_pca=coeff(:,1:dim_pca);
pca_train_feature=center_train_feature*projection_pca;
pca_test_feature=center_test_feature*projection_pca;
```

*coeff* in pca buildin function means the eigenvector space. *score* in pca buildin function means the data after transformation. *latent* means the sorted eigenvalues. After doing pca, our *train_feature* will be $2268\times495$ and *test_feature* will be $432\times495$

#### LDAReduction.m
This function strictly follow the procedure in http://sebastianraschka.com/Articles/2014_python_lda.html. The final dimension is determined by capturing the 99% variance of train data.

```
dim_lda=0;
var_percent_lda=0;
for i =1:dim_pca
    var_percent_lda=var_percent_lda+prop_d(i);
    dim_lda=dim_lda+1;
    if var_percent_lda>=0.99
        break
    end
end
```

After LDA, our dimension of feature reduce to 96 based on capturing 99% of the variance. Our *train_feature* will be $2268\times96$ and *test_feature* will be $432\times96$ eventually.


## Main2.m
We can load *train_feature.mat* and *test_feature.mat* which we saved via *Main.m*
Assign class for train and test
```
for i=1:nrow1
    train_class(i)=ceil(i/21);
end
nrow2=size(test_feature,1);
for i=1:nrow2
    test_class(i)=ceil(i/4);
end
```
Do iris matching with respect to orignial feature table and reduced feature table. Then we evaluate the performance of our implementation.


## PerformanceEvaluation.m

This function will draw two tables. One is CRR (Correct Recognition Rate) under different similarity measure. The other is graph showing CRR with respect to dimensionality of the feature vector. These two table will be drawed by *CrrTable.m* and *CRRdim.m*


What I would like to mention here is that the curve we get from *CRRdim.m* is increasing first and decreasing after 100 dimensions approximately. The reason why the graph shows like this is we have only 108 classes. When dimension of feature is larger than our number of classes, the CRR will decrease since the feature might be redundant if dimension is greater than the number of classes.

The evaluation graph is showed as *CrrTable.png* and *CRRdim.png*

# Improvement

For improvement, the most important one I think is the localization part. A good localization will show us a perfect iris area. The information we extract will be more precise. Since I implement the localization with the assumption that pupil and iris will share the same center, this assumption may produce extra error in the feature extractio step and iris matching step. We may need more time to find good parameter to do good localizaiton for all images or we need to write a explicit function that find in and out boundary on our own.
