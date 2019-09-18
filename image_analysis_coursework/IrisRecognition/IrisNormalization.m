function [normI]=IrisNormalization(I,pupil_center,pupil_radius,iris_radius,rotation)


M=64;
N=512;
normI=zeros(M,N);

for X=1:N
    for Y=1:M
        theta=2*pi*(X+rotation)/N;

        inner_x=pupil_center(1)+pupil_radius*cos(theta);
        inner_y=pupil_center(2)+pupil_radius*sin(theta);
        outer_x=pupil_center(1)+iris_radius*cos(theta);
        outer_y=pupil_center(2)+iris_radius*sin(theta);
        
        x=inner_x+(outer_x-inner_x)*Y/M;
        y=inner_y+(outer_y-inner_y)*Y/M;
        if ceil(x)>320 || ceil(y)>280 || floor(x)<=0 || floor(y)<=0
            continue
             
        else
            normI(Y,X)=interpolate(I,y,x);
        end
    end

end
        
