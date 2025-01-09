import torch
import ctranslate2

# Check if CUDA is available
print(f"CUDA available: {torch.cuda.is_available()}")

# Get the number of available GPUs
print(f"Number of GPUs: {torch.cuda.device_count()}")

# Get the name of the current GPU
if torch.cuda.is_available():
    print(f"Current GPU: {torch.cuda.get_device_name(0)}")

# Create a sample tensor and move it to GPU
x = torch.rand(5, 3)
if torch.cuda.is_available():
    x = x.cuda()
    print(f"Tensor is on GPU: {x.is_cuda}")
else:
    print("Tensor is on CPU")

# Check the device of the tensor
print(f"Device: {x.device}")

# Perform a simple operation to test GPU usage
if torch.cuda.is_available():
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    start.record()
    result = torch.matmul(x, x.t())
    end.record()

    # Waits for everything to finish running
    torch.cuda.synchronize()

    print(f"GPU computation time: {start.elapsed_time(end)} milliseconds")

# Check CTranslate2 device info
# print(
#     f"CTranslate2 GPU supported types: {ctranslate2.get_supported_compute_types('cuda')}"
# )
