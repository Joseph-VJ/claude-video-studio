"""Opt-in GPU blur: six local FP64 box sums, reflect edges and FP32 pass outputs."""
import numpy as np

def make_blur(cp):
    kernel = cp.ElementwiseKernel(
      'raw float32 src, int32 height, int32 width, int32 radius, int32 axis',
      'float32 dst', r'''
      int yy = i / width, xx = i % width;
      int dim = axis == 0 ? height : width;
      int center = axis == 0 ? yy : xx;
      int period = 2 * (dim - 1);
      double total = 0.0;
      for (int shift = -radius; shift <= radius; ++shift) {
        int pos = center + shift;
        if (dim == 1) pos = 0;
        else { pos %= period; if (pos < 0) pos += period;
               if (pos >= dim) pos = period - pos; }
        int lookup = axis == 0 ? pos * width + xx : yy * width + pos;
        total += (double)src[lookup];
      }
      dst = (float)(total / (double)(2 * radius + 1));
      ''', 'studio_mirror_box64', options=('--fmad=false',))
    def blur(a, r):
        if a.ndim != 2 or a.dtype != cp.float32 or not a.size or int(r) != r or r < 0:
            raise ValueError('Only 2D float32 inputs supported')
        a = cp.ascontiguousarray(a)
        h,w=a.shape
        for axis in (0,1):
            for repeat in range(3):
                a=kernel(a,np.int32(h),np.int32(w),np.int32(r),np.int32(axis),size=a.size).reshape(h,w)
        return a
    return blur