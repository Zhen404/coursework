function [reduce_train_feature,reduce_test_feature]=LDAReduction(train_feature,test_feature)
dim_pca=size(train_feature,2);

%LDA
%Step 1 & 2
%overall mean
overall_mean=mean(train_feature,1);
%within-class scatter
Sw=zeros(dim_pca,dim_pca);
%between-class scatter
Sb=zeros(dim_pca,dim_pca);

for i=1:108
    mean_vector_train(i,:)=mean(train_feature(((21*(i-1)+1):(21*i)),:),1);
    %within scatter each class
    W=(train_feature(((21*(i-1)+1):(21*i)),:)-mean_vector_train(i,:))'*(train_feature(((21*(i-1)+1):(21*i)),:)-mean_vector_train(i,:));
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

dim_lda=0;
var_percent_lda=0;
for i =1:dim_pca
    var_percent_lda=var_percent_lda+prop_d(i);
    dim_lda=dim_lda+1;
    if var_percent_lda>=0.99
        break
    end
end
disp(dim_lda);

projection_lda=Vs(:,1:dim_lda);
reduce_train_feature=train_feature*projection_lda;
reduce_test_feature=test_feature*projection_lda;

end
