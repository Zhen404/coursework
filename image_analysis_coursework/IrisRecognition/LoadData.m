clear all;

path='CASIA Iris Image Database (version 1.0)/';
subpath='00';

for i=1:108
    if i>=10
        subpath='0';
    end
    
    if i>=100
        subpath='';
    end
    
    for j=1:2
        
        if j==1
            for k=1:3
                filepath1=strcat(path,subpath,num2str(i),'/',num2str(j),'/',subpath,num2str(i),'_',num2str(j),'_',num2str(k),'.bmp');
                im=imread(filepath1);
                train(:,3*(i-1)+k)=reshape(im,1,280*320);
            end
        end
        
        if j==2
            for m=1:4
                filepath2=strcat(path,subpath,num2str(i),'/',num2str(j),'/',subpath,num2str(i),'_',num2str(j),'_',num2str(m),'.bmp');
                im=imread(filepath2);
                test(:,4*(i-1)+m)=reshape(im,1,280*320);
            end
        end
    end
end
save train.mat train;
save test.mat test;