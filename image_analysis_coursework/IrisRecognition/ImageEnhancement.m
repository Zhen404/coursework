function [enhanceI]=ImageEnhancement(normI)
h = 1/16*ones(16,1);
H = h*h';
imfilt = filter2(H,normI);
subtractI=normI-imfilt;
enhanceI=adapthisteq(subtractI,'NumTiles',[2,16]);

end

