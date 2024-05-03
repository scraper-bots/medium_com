class UsersController < ApplicationController
  def show
    if User.exists?(params[:id])
      @user = User.includes(:tweets, :following, :followers).find(params[:id])
      @user.tweets = @user.tweets.includes(:likers).with_attached_tweet_pic
      @likes_count = UserLike.group(:like).count
    else
      redirect_to root_path
    end
  end

  def likes
    if User.exists?(params[:id])
      @user = User.find(params[:id])
      @likes_count = UserLike.group(:like).count
    else
      redirect_to root_path
    end
  end

  def settings; end

  def settings_update
    if current_user.update(settings_params)
      redirect_to settings_path
    else
      current_user.reload
      render :settings, status: :unprocessable_entity
    end
  end

  private

  def settings_params
    params.require(:user).permit(:avatar, :username, :bio)
  end
end
