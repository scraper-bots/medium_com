# Twitter Clone

This project is a Twitter clone application built with Ruby on Rails as part of the final project in The Odin Project's Ruby on Rails course. The goal of this project is to create a simplified version of the popular social media platform, Twitter, where users can sign up, create profiles, post tweets, follow other users, and interact with their posts. Link to the course [here](https://www.theodinproject.com/lessons/ruby-on-rails-rails-final-project)

<p align=center>
<img src="https://github.com/youyoumu/twitter-clone/blob/main/preview/preview_1.png" width="720" height="auto" >
<img src="https://github.com/youyoumu/twitter-clone/blob/main/preview/preview_2.png" width="720" height="auto" >
</p>

## Feature

- Sign up and create a new account
- Sign in with Google
- Log in and log out securely
- Create and edit their user profile with avatar and bio
- Compose and publish new tweets with picture
- View a timeline of tweets from users
- Like other users' tweets
- Follow and unfollow other users

### Future plan

- [ ] Direct message
- [ ] Tag/mention other users
- [ ] Notification
- [ ] Sign in with username
- [ ] Forget/reset user password
- [ ] Change user password

## Technology Used

- Ruby on Rails
- PostgreSQL
- Bootstrap

## Dependencies

- Ruby version 3.2.2
- Postgresql
- libvips
- Yarn
- Redis

## Installation

Clone this repository
```
git clone git@github.com:youyoumu/twitter-clone.git
cd twitter-clone
```
Install required gem
```
bundle install
```
Setup database
```
rails db:create
rails db:migrate
```
Precompile assets
```
rails assets:precompile
```

## Usage
To run the app in development enviroment
```
rails server
```

## Configuration
To use Google oauth2, create `.env` in project root directory to set your `CLIENT ID` and `CLIENT SECRET`
```
GOOGLE_OAUTH_CLIENT_ID=<your_client_id>
GOOGLE_OAUTH_CLIENT_SECRET=<your_client_secret>
```

