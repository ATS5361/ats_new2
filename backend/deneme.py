try:
    import torch
    print("PyTorch başarıyla import edildi!")
except ImportError as e:
    print(f"Import Hatası: {e}")