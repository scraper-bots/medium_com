# == Schema Information
#
# Table name: user_followings
#
#  id         :bigint           not null, primary key
#  user_id    :bigint           not null
#  following  :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#
class UserFollowing < ApplicationRecord
  belongs_to :user
  belongs_to :following, class_name: 'User', foreign_key: 'following'
end
