function [ channel] = gabor_channel(x,y,deltax,deltay,f )
channel=1/((2*pi)*deltax*deltay)*exp((-1/2)*(x^2/deltax^2+y^2/deltay^2))*cos(2*pi*f*sqrt(x^2+y^2));


end

