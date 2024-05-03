class TweetsController < ApplicationController
  def index
    set_tweets
    @tweet = Tweet.new
  end

  def create
    @tweet = Tweet.new(tweet_params)
    @tweet.user = current_user
    if @tweet.content.blank?
      if @tweet.tweet_pic.attached?
        save_tweet
      else
        render_content_blank_error
      end
    else
      save_tweet
    end
  end

  def show
    @tweet = Tweet.find(params[:id])
    @tweet_reply = Tweet.new
    @likes_count = UserLike.where(like: @tweet).group(:like).count
  end

  def edit
    @tweet = Tweet.find(params[:id])
    if @tweet.user != current_user
      render plain: 'forbidden', status: :forbidden
    else
      render :edit
    end
  end

  def update
    @tweet = Tweet.find(params[:id])
    return if @tweet.user != current_user

    if params[:tweet][:content].blank?
      if @tweet.tweet_pic.attached?
        update_tweet
      else
        flash.now[:error] =
          'tweet cannot be blank without a picture.'
        @tweet.reload
        render :edit, status: :unprocessable_entity
      end
    else
      update_tweet
    end
  end

  def page
    page_size = 10
    @page = if params[:page].blank?
              1
            else
              params[:page].to_i
            end
    if User.exists?(params[:user_id])
      @user = User.find(params[:user_id])
      @last_tweet_id = if params[:last_tweet_id].blank?
                         @user.tweets.last.id
                       else
                         params[:last_tweet_id].to_i
                       end
      @tweets = Tweet.where(user_id: @user.id)
                     .where('id <= ?', (@last_tweet_id - (page_size * (@page - 1))))
                     .order(id: :desc)
                     .limit(page_size)
      @total_pages = (@user.tweets.count.to_f / page_size).ceil
    else
      @last_tweet_id = if params[:last_tweet_id].blank?
                         Tweet.last.id
                       else
                         params[:last_tweet_id].to_i
                       end
      @tweets = Tweet.where('id <= ?', (@last_tweet_id - (page_size * (@page - 1)))).order(id: :desc).limit(page_size)
      @total_pages = (Tweet.count.to_f / page_size).ceil
    end
    @likes_count = UserLike.where(like: @tweets).group(:like).count
    @tweets = @tweets.includes(:user, :likers).with_attached_tweet_pic
  end

  private

  def tweet_params
    params.require(:tweet).permit(:content, :tweet_pic, parent_attributes: [:id])
  end

  def update_params
    params.require(:tweet).permit(:content)
  end

  def save_tweet
    if @tweet.save
      Turbo::StreamsChannel.broadcast_prepend_later_to(:tweets_stream,
                                                       target: :tweets_container,
                                                       partial: 'tweets/tweet_frame',
                                                       locals: { tweet: @tweet })
      redirect_to tweet_path(@tweet)
    else
      render_error
    end
  end

  def update_tweet
    if @tweet.update(update_params)
      redirect_to tweet_path(@tweet)
    else
      @tweet.reload
      render :edit, status: :unprocessable_entity
    end
  end

  def set_tweets
    @tweets = Tweet.all.with_attached_tweet_pic.includes(:user).order(created_at: :desc)
    @likes_count = UserLike.group(:like).count
  end

  def render_show_error
    @tweet_reply = @tweet
    @tweet = @tweet.parent
    @likes_count = UserLike.where(like: @tweet).group(:like).count
    render :show, status: :unprocessable_entity
  end

  def render_content_blank_error
    flash.now[:error] =
      'tweet cannot be blank without a picture.'
    render_error
  end

  def render_index_error
    set_tweets
    render :index, status: :unprocessable_entity
  end

  def render_error
    if @tweet.parent.present?
      render_show_error
    else
      render_index_error
    end
  end
end
