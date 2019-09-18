function [pca_train_feature,pca_test_feature]=PCAReduction(train_feature,test_feature)
%PCA
%center
center_train_feature=bsxfun(@minus,train_feature,mean(train_feature));
center_test_feature=bsxfun(@minus,test_feature,mean(test_feature));

%Do pca
[coeff,score,latent]=pca(center_train_feature);
dim_pca=495;


projection_pca=coeff(:,1:dim_pca);
pca_train_feature=center_train_feature*projection_pca;
pca_test_feature=center_test_feature*projection_pca;

end