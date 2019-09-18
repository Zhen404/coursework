load train_feature.mat;
load test_feature.mat;
nrow1=size(train_feature,1);
for i=1:nrow1
    train_class(i)=ceil(i/21);
end
nrow2=size(test_feature,1);
for i=1:nrow2
    test_class(i)=ceil(i/4);
end

[pca_train_feature,pca_test_feature]=PCAReduction(train_feature,test_feature);
[reduce_train_feature,reduce_test_feature]=LDAReduction(pca_train_feature,pca_test_feature);
[predict_class1,predict_class2,predict_class3]=IrisMatching(train_feature,test_feature,train_class);
[reduce_predict_class1,reduce_predict_class2,reduce_predict_class3]=IrisMatching(reduce_train_feature,reduce_test_feature,train_class);
predict_class=[predict_class1;predict_class2;predict_class3];
reduce_predict_class=[reduce_predict_class1;reduce_predict_class2;reduce_predict_class3];
PerformanceEvaluation(predict_class,reduce_predict_class,train_class,test_class,train_feature,test_feature);
