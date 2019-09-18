function []=CrrTable(test_class,predict_class,reduce_predict_class)
test_error1=mean(test_class==predict_class(1,:));
test_error2=mean(test_class==predict_class(2,:));
test_error3=mean(test_class==predict_class(3,:));

rd_test_error1=mean(test_class==reduce_predict_class(1,:));
rd_test_error2=mean(test_class==reduce_predict_class(2,:));
rd_test_error3=mean(test_class==reduce_predict_class(3,:));

SimilarityMeasure = {'L1 distance measure';'L2 distance measure';'Cosine similarity measure'};
Original_feature=[test_error1;test_error2;test_error3];
Reduce_feature=[rd_test_error1;rd_test_error2;rd_test_error3];
T=table(SimilarityMeasure,Original_feature,Reduce_feature);
% Get the table in string form.
TString = evalc('disp(T)');
% Use TeX Markup for bold formatting and underscores.
TString = strrep(TString,'<strong>','\bf');
TString = strrep(TString,'</strong>','\rm');
TString = strrep(TString,'_','\_');
% Get a fixed-width font.
FixedWidth = get(0,'FixedWidthFontName');
% Output the table using the annotation command.
annotation(gcf,'Textbox','String',TString,'Interpreter','Tex',...
    'FontName',FixedWidth,'Units','Normalized','Position',[0 0 1 0.7]);
end