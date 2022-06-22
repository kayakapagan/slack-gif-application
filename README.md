<div id="top"></div>

[![Apache 2.0 License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://c.tenor.com/XcQKKS3ENMYAAAAd/guys-i-got-a-gif-idea-boost-the-server.gif" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">Slack Gif Application</h3>

  <p align="center">
    Gif finder application for slack which uses Giphy API.
    <br />
    <a href="https://github.com/kayakapagan/slack-gif-application/issues">Report Bug</a>
    ·
    <a href="https://github.com/kayakapagan/slack-gif-application/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li>
          <a href="#prerequisites">Prerequisites</a>
          <ul>
            <li><a href="#website-related-prerequisites">Website Related Prerequisites</a></li>
            <li><a href="#install-python">Install Python</a></li>
            <li><a href="#create-virtual-environment">Create Virtual Environment</a></li>
            <li><a href="#activate-virtual-environment-and-install-requirementstxt">Activate Virtual Environment and Install `requirements.txt`</a></li>
            <li><a href="#create-env-file">Create `.env` File</a></li>
        </ul>
        </li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#man_astronaut-show-your-support">:man_astronaut: Show your support</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a project to select a gif in an easier way to send it from slack. A slack message from my friend [Grace](https://github.com/telegrace) was the initial motivation for this project, thanks to her. Before this project you had two options, you can use Giphy's integration which gives you a random gif and you can shuffle or you can go to the website directly and copy the gif directly from there. Both metods did not seem perfect for the ease of use. So decided to write an application to solve this issue. Currently it is still not the perfect solution but planning to try different approaches. Current solution is giving you first 10 gifs from the search of Giphy API.

There is also a possibility to extend (create new one like this) this repository to collect different applications in one place as open source.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [Bolt Python](https://slack.dev/bolt-python/concepts)
* [Grip](https://github.com/joeyespo/grip)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Since this is a platform dependent project which depends on slack, we need to set some configurations on their website to use this project.

### Prerequisites

#### Website Related Prerequisites

* You need to create a new application from [here](https://api.slack.com/apps).
* Go to your application and from `Event Subscriptions` tab set `Enable Events` as `On`.
* At the same page, open `Subscribe to bot events` and add the followings:
  * app_mention
  * message.channels
  * message.groups
  * message.im
  * message.mpim
* Come to the `Slash Commands` tab and press `Create New Command` button.
* Write `/find-gif` as command and set a short description like `finds gifs`.

#### Install Python

* Make sure you have python3.6 or higher installed.

#### Create Virtual Environment

* Run the following command to create a virtual environment:

```bash
  python3 -m virtualenv venv
```

#### Activate Virtual Environment and Install `requirements.txt`

* Run the following commands to activate virtual environment and install `requirements.txt`:

```bash
  source venv/bin/activate
  pip install -r requirements.txt
```

#### Create `.env` File

* For `SLACK_SIGNING_SECRET` go to the `Basic Information` tab from your application's page.
* Scroll down to `App Credentials` and copy `Signing Secret` for the `SLACK_SIGNING_SECRET`.
* For `SLACK_APP_TOKEN` continue scrolling down to `App-Level Tokens` and press `Generate Token and Scopes` button, name it as you wish and add `connections:write` scope, then you can create the token. Copy that token and assign to `SLACK_APP_TOKEN` in the `.env` file.
* For `SLACK_BOT_TOKEN` come to `Install App` tab and see the `Bot User OAuth Token`, copy it and assign it to `SLACK_BOT_TOKEN`.
* For `GIPHY_KEY` go to [this link](https://developers.giphy.com) and press the create account since you need to have an account to get an API Key.
* After creating the account press `Create an App` button, `select API` and create your app.
* You can copy the token and assign to `GIPHY_KEY`.

#### Start the Applications

* First make sure that virtual environment (venv) is active, if not activate is with the following command:

```bash
  source venv/bin/activate
```

* After you are sure that venv is active, run the below command to start the application:

```bash
  python app.py
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Make sure application is running. Then go to your own chat or go to the chat with your application and run command `/find-gif <write your search query here without '<','>' symbols>`. Application will print 10 gifs with that search query numbered from 1 to 10 and will ask you which one you want to send. After you pick the number, application will ask which channel you want to send. Be careful, if you do not invite the application to that channel before, application cannot send the gif. So first go to that channel and invite your application with `/invite <your application name>`. After that when you select the channel, it will send the selected gif directly.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Thanks!

1. Fork the Project
2. If there is no issue about that feature/fix, first create an issue
3. Create your branch from that issue and checkout (`git checkout -b <issue number>-<issue name spaces replaced with dash>`)
4. Commit your changes with meaningfull start like "Feat:" / "Fix:" / "Refactor:" ... (`git commit -m 'Feat: Add some AmazingFeature'`)
5. Push to the Branch (`git push origin <issue number>-<issue name spaces replaced with dash>`)
6. Open a Pull Request

P.S. if you want to contribute README.md or docs, you can use `grip` it is already included to the requirements.txt file. You just need to run the command `grip` and you can preview if from your localhost.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

This project is distributed under the Apache 2.0 License. See [LICENSE](https://github.com/kayakapagan/slack-gif-application/blob/dev/LICENSE) for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

If we see the requirement for a fast paced discussion environment, we can create a slack or discord channel. At the point please create an issue about it or if the issue is already there please upvote with an emoji. Until then, you can reach me from below email address.

Kaya Kapagan - kayakapagan@sabanciuniv.edu 

Project Link: [https://github.com/kayakapagan/slack-gif-application](https://github.com/kayakapagan/slack-gif-application)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Below, you can find some resources that helped during the development, and may help you too.

* [Slack API](https://api.slack.com)
* [Bolt Python Documentation](https://slack.dev/bolt-python/tutorial/getting-started)
* [How to build a simple Slack bot using the Bolt framework for Python by `PyBites`](https://www.youtube.com/watch?v=oDoFvpDftBA)
* [Giphy API Documentation](https://developers.giphy.com/docs/api)
* [README Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#top">back to top</a>)</p>

## :man_astronaut: Show your support

Please don't forget to give a ⭐️ if you like this project! Thanks again!

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/badge/License-Apache%202.0-blue.svg
[license-url]: https://opensource.org/licenses/Apache-2.0