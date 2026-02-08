# Professional Headshot Background Replacer

Takes user uploaded amateur headshots and allows AI powered background removal and replacement

## Project Overview

This Python project shows different approaches to background removal and replacement for images. This was built as a learning project to help me understand and get hands-on experience with API integration, Git workflow, file validation, and user interaction.

## Features

- **File Validation** - Ensures only valid file types are allowed for upload
- **Intuitive GUI** - Tkinter interface allows for user image upload and selection
- **Multiple Background Choices** - Pick from three background templates
- **Three Approaches Compared** - Explores different masking and segmentation techniques

## Results Comparison

### Original Test Image
![Original Test Image](readme_images/test_HS.jpg)

### Approach 1: Basic Segmentation Using DeepLabV3
**Method:** Use MediaPipe's DeepLabV3 model with binary mask
**Result:**
![Baseline Result](readme_images/mainStruc.png)
**Pros:** Fast
**Cons:** Halo around the edge of the person form previous background

### Approach 2: Edge-Feathering
**Method:** Use cv2 Gaussian blur on mask edges
**Result:**
![Feathering Result](readme_images/edgeFeathering.png)
**Pros:** Fast, depending on the test image given it would have less of a halo
**Cons:** Halo is still visible

### Approach 3: Remove.bg API (Final)
**Method:** Use professional background remover API
**Result:**
![Remove Bg Result](readme_images/RemovebgRes.png)
**Pros:** No halo, clean edges, better quality
**Cons:** Requires internet and API credits

### Setup

1. **Clone the repository**
```bash
   git clone https://github.com/zanealadi/headshot-background-replacer.git
   cd headshot-background-replacer
```

2. **Create virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Configure API key**
   
   Create a `.env` file in the project root:
```
   REMOVEBG_API_KEY=your_api_key_here
```
   
   Get your API key at: https://www.remove.bg/api

## Usage
```bash
python main.py
```

1. Click **"Upload Headshot"** to select your image
2. Choose a professional background from the options
3. Processed image saves to `outputs/final_result.png`

## Technologies Used

- **Python 3.11** - Core language
- **OpenCV** - Image processing and manipulation
- **MediaPipe** - DeepLabV3 segmentation model
- **NumPy** - Array operations and mask handling
- **Tkinter** - Basic GUI framework
- **Remove.bg API** - Professional background removal
- **python-dotenv** - Environment variable management

## What I Learned

- **API Integration:** This was my first time learning how to use and integrate API's into projects. I learned how to use them, handle authentication, manage API keys, and debug errors.
- **Problem Solving:** I looked up different methods to solve the halo issue and learned how to implement them. I was able to learn how to balance trade-offs bewteen different methods and choose the best option
- **Computer Vision Fundamentals:** I learned about image segmentation, masking, alpha channels, and the restrictions that come with them.
- **Git Version Control:** This was my first project I was able to use Git on. This really helped me undertstand how to implement it and why it's so important. Especially since I was able to create branches based on the methods I tried throughout the project.

## Project Structure
```
headshot_maker/
├── main.py                 # Main application file
├── models/                 # DeepLabV3 model file
├── backgrounds/            # Professional background images
├── outputs/               # Generated results
├── test_images/           # Sample test images
├── .env                   # API key (not committed)
├── requirements.txt       # Python dependencies
└── README.md
```

## Git Branches

- `master` - Baseline DeepLabV3 implementation
- `edge-feathering` - Gaussian blur edge refinement
- `removebg-api` - Professional API integration (current)

## Future Improvements

- [ ] Batch processing for multiple images
- [ ] Drag-and-drop file upload
- [ ] Custom background upload option
- [ ] Real-time preview
- [ ] Export to different formats/sizes based on user preferences
- [ ] Web interface (Flask/Streamlit)

## License

MIT

## Acknowledgments

- MediaPipe team for segmentation models
- Remove.bg for their API