"""Isolated E: GPU runtime; never replaces the shared CPU ONNX installation."""
from pathlib import Path
import os,sys,ctypes
ROOT=Path("E:/Video")
_HANDLES=[];_DLLS=[]
def prepare_cuda():
    roots=[ROOT/".venv/Lib/site-packages/nvidia",ROOT/"tools/onnx-gpu-cuda/nvidia"]
    dirs=[p for root in roots for p in root.glob("*/bin")]
    os.environ["PATH"]=";".join(str(p) for p in dirs)+";"+os.environ.get("PATH","")
    for p in dirs:_HANDLES.append(os.add_dll_directory(str(p)))
    for name in ["nvrtc64_120_0.dll","cublasLt64_12.dll","cublas64_12.dll","cudart64_12.dll","nvJitLink_120_0.dll","cufft64_11.dll","cudnn64_9.dll"]:
        path=next((d/name for d in dirs if (d/name).exists()),None)
        if path:_DLLS.append(ctypes.WinDLL(str(path)))
    os.environ.setdefault("CUDA_CACHE_PATH",str(ROOT/"cache/cuda"))
    os.environ.setdefault("CUPY_CACHE_DIR",str(ROOT/"cache/cupy"))
    os.environ.setdefault("CUDA_PATH",str(ROOT/"tools/onnx-gpu-cuda/nvidia/cuda_runtime"))
def load_ort(gpu=True):
    if gpu:
        prepare_cuda();location=ROOT/"tools/onnx-gpu"
        if "onnxruntime" in sys.modules and not str(sys.modules["onnxruntime"].__file__).startswith(str(location)):
            raise RuntimeError("Start a fresh Python process before selecting the isolated GPU runtime")
        sys.path.insert(0,str(location))
    import onnxruntime as ort
    return ort
def matting_session(gpu=True,threads=2):
    ort=load_ort(gpu);o=ort.SessionOptions();o.intra_op_num_threads=threads;o.inter_op_num_threads=1;o.log_severity_level=3
    providers=[("CUDAExecutionProvider",{"cudnn_conv_algo_search":"DEFAULT","cudnn_conv_use_max_workspace":"0","use_tf32":"0","gpu_mem_limit":1610612736}),"CPUExecutionProvider"] if gpu else ["CPUExecutionProvider"]
    s=ort.InferenceSession(str(ROOT/"models/rvm/rvm_mobilenetv3_fp32.onnx"),sess_options=o,providers=providers)
    if gpu:
        s.disable_fallback()
        if "CUDAExecutionProvider" not in s.get_providers():raise RuntimeError("CUDA inactive; CPU fallback is not a GPU result")
    return s
def load_cupy():
    prepare_cuda();sys.path.insert(0,str(ROOT/"tools/cupy-gpu"))
    import cupy
    cupy.get_default_memory_pool().set_limit(size=768*1024*1024)
    return cupy
