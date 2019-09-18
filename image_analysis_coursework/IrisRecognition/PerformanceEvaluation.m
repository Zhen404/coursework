function []=PerformanceEvaluation(predict_class,reduce_predict_class,train_class,test_class,train_feature,test_feature)
CrrTable(test_class,predict_class,reduce_predict_class);
CRRdim(train_feature,test_feature,train_class,test_class);
end