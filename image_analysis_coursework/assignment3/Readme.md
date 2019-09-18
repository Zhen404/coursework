
# Logic and Parameter Introduction

The parameter we can change:

1. Thershold
2. C in svm
3. gamma in svm
4. random state
5. PCA dimension(PCA+SVM part)

Since the size of our data is small, SVM fluctuates a lot given different split. The way we split matters too much. In my work for each dataset, I first loop over C in svm
```
scores=[]
index=[]

for c in [0.01,0.1,1,10,100]:
    clf=SVC(kernel='linear',C=c,gamma=100)
    clf.fit(X_train,y_train)
    index.append(c)
    scores.append(clf.score(X_test,y_test))
```
From the graph I plot, there is no change in score. I also try gamma=0.01. There is also no change in score. 

Then I loop over random state to find a split with good score.
```
for i in range(1,150):
    train,test=train_test_split(fmri_ROI_df,test_size=0.5,random_state=i)
```

Finally, with the best split, I add the PCA procedure. I loop over the number of principle component in PCA using the **scaled** train and test set to find the best PCA dimension
```
for i in range(10,150):
    pca = PCA(n_components=i)
    pca.fit(X_train)
    X_train_pca= pca.transform(X_train)
    X_test_pca=pca.transform(X_test)

    clf2=SVC(kernel='linear',C=0.01,gamma=0.01)
    clf2.fit(X_train_pca,y_train)
    
    
    index.append(i)
    scores.append(clf2.score(X_test_pca,y_test))
```

I run the same procedure for four datasets.

1. sub-01/ses-test Data (Threshold=500)
2. sub-01/ses-test Data (Threshold=800)
3. sub-01/ses-retest Data (Threshold=500)
4. sub-01/ses-retest Data (Threshold=800)

# Result


### sub-01/ses-test Data (Threshold=500)
1. SVM only

**Trial**: SVM(c=0.01, gamma=0.01)<br/>
**Accuracy**: 0.8478260869565217<br/>
**Trial(best)**: SVM(c=0.01,gamma=0.01), random_state=115<br/>
**Accuracy**: 0.9239130434782609<br/>
**Predict Label**: [1 4 4 4 3 1 4 1 2 1 4 2 1 1 1 4 1 3 2 2 4 1 3 2 2 1 1 2 3 1 1 1 1 4 2 1 4
 1 1 1 1 1 1 1 1 1 1 1 4 3 1 1 1 3 3 1 1 1 4 3 1 1 1 1 1 4 1 2 2 2 4 3 1 1
 2 1 4 3 4 2 1 4 4 4 2 1 1 1 4 1 1 2]<br/>
**Real Label**: [2 4 4 4 3 3 4 1 2 1 4 2 1 1 1 4 1 3 2 1 4 1 3 2 2 1 1 2 3 1 1 1 1 4 2 1 4
 1 1 1 1 1 1 1 1 1 1 2 4 3 1 1 1 3 3 1 1 1 4 3 1 1 1 1 1 4 1 1 2 2 4 3 1 1
 2 1 1 3 4 2 1 4 4 4 2 1 1 1 4 1 3 2]
2. PCA+SVM

**Trial(best)**: PCA (components = 78), SVM(c=0.01,gamma=0.01), random_state=115<br/>
**Accuracy**: 0.9347826086956522<br/>
**Predict Label**: [1 4 4 4 3 3 4 1 2 1 4 2 1 1 1 4 1 3 2 2 4 1 3 2 2 1 1 2 3 1 1 1 1 4 2 1 4
 1 1 1 1 1 1 1 1 1 1 2 4 3 1 1 1 3 1 1 1 1 4 3 1 1 1 1 1 4 1 1 2 2 4 3 1 1
 2 1 1 3 4 1 1 4 4 4 1 1 1 1 4 1 1 2]<br/>
**Real Label**: [2 4 4 4 3 3 4 1 2 1 4 2 1 1 1 4 1 3 2 1 4 1 3 2 2 1 1 2 3 1 1 1 1 4 2 1 4
 1 1 1 1 1 1 1 1 1 1 2 4 3 1 1 1 3 3 1 1 1 4 3 1 1 1 1 1 4 1 1 2 2 4 3 1 1
 2 1 1 3 4 2 1 4 4 4 2 1 1 1 4 1 3 2]


### sub-01/ses-test Data (Threshold=800)
1. SVM only

**Trial**: SVM(c=0.01, gamma=0.01)<br/>
**Accuracy**: 0.8152173913043478<br/>
**Trial(best)**: SVM(c=0.01,gamma=0.01), random_state=71<br/>
**Accuracy**: 0.9347826086956522<br/>
**Predict Label**: [1 2 1 4 1 1 3 2 1 3 4 1 2 3 1 1 3 4 1 1 2 1 4 4 2 1 2 3 1 1 1 1 1 1 1 1 1
 3 4 1 4 1 1 2 1 4 3 1 1 1 3 1 4 1 1 4 1 2 1 3 1 1 4 1 1 2 1 3 4 4 1 1 1 4
 1 1 1 1 3 1 4 1 3 2 3 1 1 3 1 1 2 1]<br/>
**Real Label**: [1 2 1 4 1 1 3 2 1 3 4 1 2 3 1 1 3 4 1 1 2 2 4 4 2 1 2 3 2 1 1 1 1 1 1 2 1
 3 4 1 4 1 1 2 1 4 3 1 1 1 3 1 4 1 1 4 1 1 1 3 1 2 4 1 1 2 1 3 4 4 1 1 1 4
 1 1 1 1 3 1 4 1 3 2 3 1 1 1 1 1 2 1]
2. PCA+SVM

**Trial(best)**: PCA (components = 67), SVM(c=0.01,gamma=0.01), random_state=71<br/>
**Accuracy**: 0.9456521739130435<br/>
**Predict Label**: [1 2 1 4 1 1 3 1 1 3 4 1 1 3 1 1 3 4 1 1 2 1 4 4 2 1 2 3 1 1 1 1 1 1 1 1 1
 3 4 1 4 1 1 2 1 4 3 1 1 1 3 1 4 1 1 4 1 2 1 3 1 1 4 1 1 2 1 3 4 4 1 1 1 4
 1 1 1 1 3 1 4 1 3 2 3 1 1 1 1 1 2 1]<br/>
**Real Label**: [1 2 1 4 1 1 3 2 1 3 4 1 2 3 1 1 3 4 1 1 2 2 4 4 2 1 2 3 2 1 1 1 1 1 1 2 1
 3 4 1 4 1 1 2 1 4 3 1 1 1 3 1 4 1 1 4 1 1 1 3 1 2 4 1 1 2 1 3 4 4 1 1 1 4
 1 1 1 1 3 1 4 1 3 2 3 1 1 1 1 1 2 1]
### sub-01/ses-retest Data (Threshold=500)
1. SVM only

**Trial**: SVM(c=0.01, gamma=0.01)<br/>
**Accuracy**: 0.717391304347826<br/>
**Trial(best)**: SVM(c=0.01,gamma=0.01), random_state=83<br/>
**Accuracy**: 0.8586956521739131<br/>
**Predict Label**: [1 4 2 1 2 1 1 1 3 1 2 3 3 4 1 1 1 1 1 3 1 1 4 1 1 2 1 1 2 1 1 1 2 1 2 3 3
 1 4 1 2 1 4 1 4 1 2 4 1 2 1 1 3 1 1 1 4 3 1 1 4 1 2 1 1 1 2 1 1 1 1 1 1 1
 4 1 1 4 1 3 1 2 3 2 2 2 4 3 1 3 1 1]<br/>
**Real Label**: [1 1 2 1 2 1 1 1 3 1 1 3 3 4 1 1 1 1 1 3 1 1 4 1 1 2 2 1 2 1 1 1 2 1 2 3 3
 1 4 1 2 1 4 1 4 1 4 1 3 1 1 4 3 1 1 1 4 3 1 1 4 1 1 1 1 1 2 1 1 1 1 1 1 4
 4 1 1 4 1 3 1 2 3 2 2 2 4 3 2 1 1 2]
2. PCA+SVM

**Trial(best)**: PCA (components = 84), SVM(c=0.01,gamma=0.01), random_state=83<br/>
**Accuracy**: 0.8260869565217391<br/>
**Predict Label**: [1 4 2 1 1 1 1 1 3 1 2 3 3 4 1 1 1 1 1 3 1 1 4 1 1 1 1 1 1 1 1 1 1 1 2 3 3
 1 4 1 2 1 4 1 4 1 2 1 1 4 1 4 3 1 1 1 1 3 1 1 4 1 2 1 1 1 2 1 1 1 1 1 1 1
 4 1 1 4 1 3 1 2 3 2 2 2 4 3 1 3 1 1]<br/>
**Real Label**: [1 1 2 1 2 1 1 1 3 1 1 3 3 4 1 1 1 1 1 3 1 1 4 1 1 2 2 1 2 1 1 1 2 1 2 3 3
 1 4 1 2 1 4 1 4 1 4 1 3 1 1 4 3 1 1 1 4 3 1 1 4 1 1 1 1 1 2 1 1 1 1 1 1 4
 4 1 1 4 1 3 1 2 3 2 2 2 4 3 2 1 1 2]
### sub-01/ses-retest Data (Threshold=800)
1. SVM only

**Trial**: SVM(c=0.01, gamma=0.01)<br/>
**Accuracy**: 0.6739130434782609<br/>
**Trial(best)**: SVM(c=0.01,gamma=0.01), random_state=83<br/>
**Accuracy**: 0.8478260869565217<br/>
**Predict Label**: [1 4 2 1 2 1 1 1 3 1 2 3 3 4 1 1 1 1 1 3 1 1 4 1 1 2 1 1 2 1 1 1 2 1 2 3 3
 1 4 1 2 1 4 1 4 1 2 4 1 2 1 4 3 1 1 1 1 3 1 1 4 1 2 1 1 1 2 1 2 1 1 1 1 1
 4 1 1 4 1 3 1 2 3 2 2 2 4 3 1 3 1 1]<br/>
**Real Label**: [1 1 2 1 2 1 1 1 3 1 1 3 3 4 1 1 1 1 1 3 1 1 4 1 1 2 2 1 2 1 1 1 2 1 2 3 3
 1 4 1 2 1 4 1 4 1 4 1 3 1 1 4 3 1 1 1 4 3 1 1 4 1 1 1 1 1 2 1 1 1 1 1 1 4
 4 1 1 4 1 3 1 2 3 2 2 2 4 3 2 1 1 2]
2. PCA+SVM

**Trial(best)**: PCA (components = 85), SVM(c=0.01,gamma=0.01), random_state=83<br/>
**Accuracy**: 0.8260869565217391<br/>
**Predict Label**: [1 4 2 1 1 1 1 1 3 1 2 3 3 4 1 1 1 1 1 3 1 1 4 1 1 1 1 1 1 1 1 1 1 1 2 3 3
 1 4 1 2 1 4 1 4 1 2 1 1 4 1 4 3 1 1 1 1 3 1 1 4 1 2 1 1 1 2 1 1 1 1 1 1 1
 4 1 1 4 1 3 1 2 3 2 2 2 4 3 1 3 1 1]<br/>
**Real Label**: [1 1 2 1 2 1 1 1 3 1 1 3 3 4 1 1 1 1 1 3 1 1 4 1 1 2 2 1 2 1 1 1 2 1 2 3 3
 1 4 1 2 1 4 1 4 1 4 1 3 1 1 4 3 1 1 1 4 3 1 1 4 1 1 1 1 1 2 1 1 1 1 1 1 4
 4 1 1 4 1 3 1 2 3 2 2 2 4 3 2 1 1 2]

# Limitation

The limitation is that the data size is relatively small. Such small size can not maintain the robust of classification algorithm. As I did in this homework, the way we split the dataset affect the accuracy a lot. The way we improve the performance is to gather more fMRI data. Although the price to get fMRI is much, including time and money, it is still necessary to get more data to help us understand our brain much better.

# Comparison

From the result, we notice that when SVM has already done a good job in classification, PCA procedure can imporve the performance only a little bit not that too much. However, when SVM cannot do a great job in classification, PCA can reduce redundant information of our data so that help us to get a better performance.
