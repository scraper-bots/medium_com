# == Schema Information
#
# Table name: user_likes
#
#  id         :bigint           not null, primary key
#  user_id    :bigint           not null
#  like       :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#
class UserLike < ApplicationRecord
  belongs_to :user
  belongs_to :tweet, foreign_key: 'like'
end
