function [predict_class1,predict_class2,predict_class3]=IrisMatching(train_feature,test_feature,train_class)
nrow1=size(train_feature,1);
nrow2=size(test_feature,1);

for i=1:nrow2
    for j=1:nrow1
        dist1(i,j)=sum(abs(train_feature(j,:)-test_feature(i,:)));
    end
    [v,ind]=min(dist1(i,:));
    predict_class1(i)=train_class(ind);
end

for i=1:nrow2
    for j=1:nrow1
        dist2(i,j)=sqrt(sum((train_feature(j,:)-test_feature(i,:)).^2));
    end
    [v,ind]=min(dist2(i,:));
    predict_class2(i)=train_class(ind);
end

for i=1:nrow2
    for j=1:nrow1
        dist3(i,j)=1-train_feature(j,:)*test_feature(i,:)'/(norm(train_feature(j,:))*norm(test_feature(i,:)));
    end
    [v,ind]=min(dist3(i,:));
    predict_class3(i)=train_class(ind);
end
end
