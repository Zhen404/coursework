
# Image preprocessing

### **Realign**

Realign is motion correction. We acquisite a series of images by doing experiment for a person. We can't guarantee the person stay still in the whole experiment. So this will cause images not in the same position. Realigning allows us to place the brain in the same position so that we can easily do the following process and analytics. Here we take 84 (16~99) images in this procedure. After Realignment, *meanfM00223_016.img* has been created

### **Coregistration**

Coregistraion is an alignment combining anatomical and functional scans. We match our mean functional scans (*meanfM00223_016.img*) to our structural image (*sM00223_002.img*) and make the experiment image more clear.

### **Segmentation**

Segmentation helps us to figure out different tissues in images. For example, spm segmentation helps us extract gray matter and white matter from the image. Spm segmentation also provide a bias corrected structure image (*msM0023_002.nii*).

### **Normalization**

This procedure is to reflect functional images into a standard space. In the standard space, there is no anatomical information. However it contains precise position information of functional images.It maintains the consistancy of the coordinate system for statistical report. This is helpful for further statistical analysis. Besides, the average signal intensity of the mean image of the functional image changes with time and has nothing to do with the functional activity. Thus the response of each stimulus is not at the same level. Normalization reduces the effect of statistical detection function activation information.

### **Smoothing**

In the experiment, it is inevitable to encounter improper signals for hardware instability and physiological motion, which we call is noise. Smoothing applies 3D guassian filter (FWHM range) to blur the image so that such noise is approximately removed from images.

# Limitation and Improvement

### Limitation

For smoothing part, we only apply [6,6,6] filter to remove the noise caused by some hardware instability and physiological motion. There are a lot of other kinds of noise. For example, time drift could produce low frequent noise. Heart beats and breathing may also produce noise in our image. 

Besides, the preprocessing procedure does not consider that fact that BOLD signals at different layers are acquired at different time. There is a time lag showing in the picture corresponding to an identical underlying problem.

### Improvement

For the low frequent noise caused by time drift. We may use a small range of FWHM, for example, 2~3mm or some low frequency filter to remove those kinds of noise.

To improve the slice timing problem, we can do slice timing correction after realignment.

# Statistical Analysis

According to the inference table **figure 30.15** in the **figures folder**, the right part are the coordinate [x,y,z]. And then we mainly focus on peak-level and cluster-level. I think peak-level takes into account the peak height only while cluster level takes into account both the peak height and the spatial extent of the cluster. 

The table returns those points which either peak-level or cluster-level has significant response to auditory stimuli. We can see all points in peak-level are significant. When we click the points in spm, corresponding red arrows will show up in the corresponding brain region above. For cluster-level, we notice the last six points are not significant because p-value is greater than 0.05, which means, in terms of cluster-level, these points are not significant. In this inference step we will take the union of the significance result
