function [matrix]=gabor_matrix(filtersize,deltax,deltay,f)
matrix=zeros(filtersize,filtersize);
height=floor(filtersize/2);
width=floor(filtersize/2);
for y=-height:height
    for x=-width:width
        matrix(height+y+1,width+x+1)=gabor_channel(x,y,deltax,deltay,f);
    end
end

end