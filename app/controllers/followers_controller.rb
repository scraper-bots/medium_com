class FollowersController < ApplicationController
  def show
    @user = User.find(params[:user_id])
    @followers = User.find(params[:user_id]).followers
  end
end
