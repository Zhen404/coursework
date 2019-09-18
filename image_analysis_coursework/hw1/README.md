
# **Workflow**

1. Input the image
2. Convert RGB channel to LAB channel
3. Take the a, b direction color information and reshape them so that they can be plugged into the k-means function
4. We find the label of each pixel in the picture
5. Draw the red detection rectangular over face

# **Code Explanation**
```
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from skimage import data
from skimage import color
from sklearn.cluster import KMeans
import pandas as pd

#read image
img=data.imread('face_d2.jpg')

plt.imshow(img)
plt.show()
``` 
In this chunk, we import all libraries we need in our code and input the the image we need to deal with.

```
#convert rgb to lab and reshape the ab information so that they can be used in kmeans
img_lab=color.rgb2lab(img)
ab=img_lab[:,:,1:3]
nrows,ncols=ab.shape[0:2]
ab=ab.reshape(nrows*ncols,2)

#kmeans cluster
img_kmeans=KMeans(n_clusters=2,random_state=1).fit(ab)

#reshape the label so that we can show the label-based image
img_seg=img_kmeans.labels_.reshape(nrows,ncols)

plt.imshow(img_seg)
plt.show()
```
In this chunk, we do K-means over a and b color information. Before that we use **_reshape()_** function prepare ab color information so that they can be plugged into **_KMeans()_** function. We choose **n_cluster** as 2. We classifiy all pixels into 2 cluster. For parameter **random_state**, we choose 1 so that the pixels of the face is labeled as 1. Then we revert the labels we obtained to a matrix which can be shown as an image.

```
#prepare output label as data frame to draw detection rectangular over face
output=pd.DataFrame(img_kmeans.labels_.reshape(nrows,ncols))

output['rowsum']=output.sum(axis=1)
output.loc['colsum'] = output.apply(lambda x: x.sum())
output.loc['colsum','rowsum']=0

#find the maximum of label 1 based on rows and columns; Also their index respectively
idmax_column=output.loc['colsum'].argmax()
idmax_row=output['rowsum'].argmax()
max_column=output.loc['colsum'].max()
max_row=output['rowsum'].max()

#find the boundary of face over columns
index_first=True
lower_col=0
while(index_first):
    if(output.loc[89,lower_col]==0):
        lower_col+=1
    else:
        index_first=False
upper_col=lower_col+max_row

#find the boundary of face over rows
index_first=True
lower_row=0
while(index_first):
    if(output.loc[lower_row,119]==0):
        lower_row+=1
    else:
        index_first=False
upper_row=lower_row+max_column

#draw the output with red detection rectangular
result=img
for row_index in range(result.shape[0]):
    for col_index in range(result.shape[1]):
        if row_index==lower_row or row_index==upper_row:
            if col_index>=lower_col and col_index<=upper_col:
                result[row_index][col_index][0]=255
                result[row_index][col_index][1]=0
                result[row_index][col_index][2]=0
        if col_index==lower_col or col_index==upper_col:
            if row_index>=lower_row and row_index<=upper_row:
                result[row_index][col_index][0]=255
                result[row_index][col_index][1]=0
                result[row_index][col_index][2]=0
                
plt.imshow(result)
plt.show()
```
In this chunk, we draw the red detection rectangular. What I do first is finding out the maximum number of label 1 for columns and rows and returning their indexes respectively, since I notice the face we recognize is the largest part of label 1. Thus, we assume the center of face is located in **_(idmax_row,idmax_column)_**. Then, based on the center of face, we find the first appearance of 1 in **_row=idmax_row_** and the first appearance of 1 in **_column=idmax_column_** as the *lower_row_bound* and *lower_column_bound*. Then, using the maximum number of 1s for columns and rows, we obtain *upper_row_bound* and *upper_column_bound*. We now have four boundaries of the rectangler. Finally, using the **_for loop_**, we exhaust all pixels in the image, set red channel as 255 and other channels as 0 and obtain the red detection rectangular in the image.

# **Limitation**

1. When we see the segmentation image, using K-means we cannot avoid classifying the left bottom hair and the figure near face part as the same cluster of face. I consider using filter like median filter over original image. But from the aspect of principle of median filter, the hair part will still be hair. The only change is that the color of hair will be smooth but such change cannot affect the result of k-means cluster. Therefore, K-means may be not a perfect way to segment face in a picture from my point of view.

2. As we see, the result image includes the neck in the red rectangular. The way to draw the rectangular can be improved. The way I use is not reproducible and not effective if the image have multiple faces or some other parts whose color is very similar to the face.


```python

```
