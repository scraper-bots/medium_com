class LikesController < ApplicationController
  def create
    current_user.likes << Tweet.find(params[:tweet_id])
  rescue ActiveRecord::RecordNotUnique
    # do nothing
  end

  def destroy
    current_user.likes.delete(Tweet.find(params[:tweet_id]))
  end

  def show
    @tweet = Tweet.find(params[:tweet_id])
  end
end
