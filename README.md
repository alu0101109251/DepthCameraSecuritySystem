<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![CC License][license-shield]][license-url]



<!-- TABLE OF CONTENTS -->
## Table of Contents

- [1. About The Project](#about-the-project)
    * [Built With](#built-with)
- [2. Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
- [3. Usage](#usage)
- [4. Roadmap](#roadmap)
- [5. Contributing](#contributing)
- [6. License](#license)
- [7. Contact](#contact)
- [8. Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

The main objective of this work is the development of a security system which allows real time monitoring 
of people's location.

Using a depth camera as well as image processing libraries such as OpenCV, it is proposed to define a safe area where 
a person can move freely, establishing a tracking system with alarm alerts integrated to trigger in cases where he 
could go out of bounds of the risk free enclosure. 



### Built With

* [OpenCV](https://pypi.org/project/opencv-python/)
* [Intel RealSense SDK](https://pypi.org/project/pyrealsense2/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* pipenv
  ```sh
  pip install pipenv
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/alu0101109251/DepthCameraSecuritySystem.git
   ```
2. Install PipEnv packages
   ```sh
   pipenv install
   ```



<!-- USAGE EXAMPLES -->
## Usage

There are 3 main scripts implemented, using different motion detection and tracking techniques.

Depending on the situation and scenario, choose the approach which works better for you.



### Absolute Difference Motion Detection



### MOG2 Subtractor Motion Detection



### CSRT Motion Tracking


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/alu0101109251/DepthCameraSecuritySystem/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the _Creative Commons Attribution-ShareAlike 4.0 International License_. 

[![CC BY-SA 4.0][license-img]][license-url]

See [`LICENSE`](LICENSE) for more information.



<!-- CONTACT -->
## Contact

Javier Alonso Delgado  - alu0101109251@ull.edu.es

Project Link: [https://github.com/alu0101109251/DepthCameraSecuritySystem](https://github.com/alu0101109251/DepthCameraSecuritySystem)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [numpy](https://numpy.org/)
* [Shields.io](https://img.shields.io/)



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/alu0101109251/DepthCameraSecuritySystem.svg?style=for-the-badge
[contributors-url]: https://github.com/alu0101109251/DepthCameraSecuritySystem/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/alu0101109251/DepthCameraSecuritySystem.svg?style=for-the-badge
[forks-url]: https://github.com/alu0101109251/DepthCameraSecuritySystem/network/members
[stars-shield]: https://img.shields.io/github/stars/alu0101109251/DepthCameraSecuritySystem.svg?style=for-the-badge
[stars-url]: https://github.com/alu0101109251/DepthCameraSecuritySystem/stargazers
[issues-shield]: https://img.shields.io/github/issues/alu0101109251/DepthCameraSecuritySystem.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo/issues
[license-shield]: https://img.shields.io/github/license/alu0101109251/DepthCameraSecuritySystem.svg?style=for-the-badge
[license-url]: http://creativecommons.org/licenses/by-sa/4.0/
[license-img]: https://licensebuttons.net/l/by-sa/4.0/88x31.png