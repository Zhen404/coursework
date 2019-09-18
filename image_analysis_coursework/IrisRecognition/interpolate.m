function normimg = interpolate( img,x,y )

xf=floor(x);
yf=floor(y);
xc=ceil(x);
yc=ceil(y);

if xf==xc && yf==yc
    normimg=img(xc,yc);
elseif xf==xc
    normimg=img(xf,yf)+(y-yf)*(img(xf,yc)-img(xf,yf));
elseif yf==yc
    normimg=img(xf,yf)+(x-xf)*(img(xc,yf)-img(xf,yf));
else
    A=[ xf, yf, xf*yf, 1
        xf, yc, xf*yc, 1
        xc, yf, xc*yf, 1
        xc, yc, xc*yc, 1];
    r=[ img(xf,yf)
        img(xf,yc)
        img(xc,yf)
        img(xc,yc)];
    a=A\double(r);
    w=[x,y,x*y,1];
    normimg=w*a;
end
end

