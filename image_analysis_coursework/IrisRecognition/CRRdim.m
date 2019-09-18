function []=CRRdim(train_feature,test_feature,train_class,test_class)
nrow1=size(train_feature,1);
for i=1:nrow1
    train_class(i)=ceil(i/21);
end
nrow2=size(test_feature,1);
for i=1:nrow2
    test_class(i)=ceil(i/4);
end
[pca_train_feature,pca_test_feature]=PCAReduction(train_feature,test_feature);
dim_pca=495;

    
%LDA
%Step 1 & 2
%overall mean
overall_mean=mean(pca_train_feature,1);
%within-class scatter
Sw=zeros(dim_pca,dim_pca);
%between-class scatter
Sb=zeros(dim_pca,dim_pca);

for i=1:108
    mean_vector_train(i,:)=mean(pca_train_feature(((21*(i-1)+1):(21*i)),:),1);
    %within scatter each class
    W=(pca_train_feature(((21*(i-1)+1):(21*i)),:)-mean_vector_train(i,:))'*(pca_train_feature(((21*(i-1)+1):(21*i)),:)-mean_vector_train(i,:));
    Sw=Sw+W;
    B=21.*(mean_vector_train(i,:)-overall_mean)'*(mean_vector_train(i,:)-overall_mean);
    Sb=Sb+B;
end



%Step 3
A=inv(Sw)*Sb;
[V,D]=eig(A);
[d,ind]=sort(diag(D),'descend');
Ds=D(ind,ind);
Vs=V(:,ind);

prop_d=d/sum(d);


dim_lda=30;
for k=1:10

projection_lda=Vs(:,1:dim_lda);
reduce_train_feature=pca_train_feature*projection_lda;
reduce_test_feature=pca_test_feature*projection_lda;

for i=1:nrow2
    for j=1:nrow1
        dist(i,j)=1-reduce_train_feature(j,:)*reduce_test_feature(i,:)'/(norm(reduce_train_feature(j,:))*norm(reduce_test_feature(i,:)));
    end
    [v,ind]=min(dist(i,:));
    predict_class(i)=train_class(ind);
end
crr_list(:,k)=mean(predict_class==test_class);
dim_list(:,k)=dim_lda;
dim_lda=30+20*k;

end
figure(2)
plot(dim_list,crr_list);
title('CRR againt Dimenshionality of feature');
xlabel('Dimension')
ylabel('CRR');
end