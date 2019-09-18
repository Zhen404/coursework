function draw_circle(x,y,radius,c)

% x,y-center of circle
% a-width of circle
% b-height of circle
% c-color of circle

th=0:pi/50:2*pi;
xunit=radius*cos(th)+x;
yunit=radius*sin(th)+y;
hold on;
plot(xunit,yunit,c);
hold off;
end