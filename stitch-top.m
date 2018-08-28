im1=imread('0.jpg');
im2=imread('1.jpg');
x1 = [1276; 2503; 2384; 1157];
y1 = [2706; 2662; 91; 135];
x2 = [1276; 2503; 2384; 1188];
y2 = [2706; 2662; 91; 122];
T=maketform('projective',[x2 y2],[x1 y1]);
T.tdata.T
[im2t,xdataim2t,ydataim2t]=imtransform(im2,T);
xdataout=[min(1,xdataim2t(1)) max(size(im1,2),xdataim2t(2))];
ydataout=[min(1,ydataim2t(1)) max(size(im1,1),ydataim2t(2))];
im2t=imtransform(im2,T,'XData',xdataout,'YData',ydataout);
im1t=imtransform(im1,maketform('affine',eye(3)),'XData',xdataout,'YData',ydataout);
ims=max(im1t,im2t);
imwrite(ims,'0+1.jpg');

im3=imread('0+1.jpg');
im4=imread('2.jpg');
info = imfinfo('2.jpg')
if info.Height < info.Width
    im4 = imrotate(im4, -90);
end
x3 = [1330; 2557; 2439; 1211];
y3 = [2728; 2682; 112; 155];
x4 = [1389; 2601; 2577; 1342];
y4 = [4750; 4723; 2094; 2119];
T2=maketform('projective',[x4 y4],[x3 y3]);
T2.tdata.T
[im4t,xdataim4t,ydataim4t]=imtransform(im4,T2);
xdataout_1=[min(1,xdataim4t(1)) max(size(im3,2),xdataim4t(2))];
ydataout_1=[min(1,ydataim4t(1)) max(size(im3,1),ydataim4t(2))];
im4t=imtransform(im4,T2,'XData',xdataout_1,'YData',ydataout_1);
im3t=imtransform(im3,maketform('affine',eye(3)),'XData',xdataout_1,'YData',ydataout_1);
ims_1=max(im3t,im4t);
imwrite(ims_1,'0+1+2.jpg');

im5=imread('0+1+2.jpg');
im6=imread('3.jpg');
info = imfinfo('3.jpg')
if info.Height < info.Width
    im6 = imrotate(im6, -90);
end
x5 = [1371; 2601; 2496; 1310];
y5 = [2047; 2004; 180; 358];
x6 = [1355; 2581; 2519; 1287];
y6 = [4105; 4103; 2135; 2341];
T3=maketform('projective',[x6 y6],[x5 y5]);
T3.tdata.T
[im6t,xdataim6t,ydataim6t]=imtransform(im6,T3);
xdataout_2=[min(1,xdataim6t(1)) max(size(im5,2),xdataim6t(2))];
ydataout_2=[min(1,ydataim6t(1)) max(size(im5,1),ydataim6t(2))];
im6t=imtransform(im6,T3,'XData',xdataout_2,'YData',ydataout_2);
im5t=imtransform(im5,maketform('affine',eye(3)),'XData',xdataout_2,'YData',ydataout_2);
ims_2=max(im5t,im6t);
imwrite(ims_2,'0+1+2+3.jpg');


im7=imread('0+1+2+3.jpg');
im8=imread('4.jpg');
info = imfinfo('4.jpg')
if info.Height < info.Width
    im8 = imrotate(im8, -90);
end
x7 = [1438; 2596; 2540; 1416];
y7 = [1145; 1139; 277; 261];
x8 = [1312; 2316; 2292; 1297];
y8 = [5135; 5096; 4229; 4262];
T4=maketform('projective',[x8 y8],[x7 y7]);
T4.tdata.T
[im8t,xdataim8t,ydataim8t]=imtransform(im8,T4);
xdataout_3=[min(1,xdataim8t(1)) max(size(im7,2),xdataim8t(2))];
ydataout_3=[min(1,ydataim8t(1)) max(size(im7,1),ydataim8t(2))];
im8t=imtransform(im8,T4,'XData',xdataout_3,'YData',ydataout_3);
im7t=imtransform(im7,maketform('affine',eye(3)),'XData',xdataout_3,'YData',ydataout_3);
ims_3=max(im7t,im8t);
imwrite(ims_3,'0+1+2+3+4.jpg');