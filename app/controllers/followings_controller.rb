class FollowingsController < ApplicationController
  def show
    @user = User.find(params[:user_id])
    @followings = User.find(params[:user_id]).following
  end
end
