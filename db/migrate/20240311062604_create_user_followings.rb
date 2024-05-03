class CreateUserFollowings < ActiveRecord::Migration[7.1]
  def change
    create_table :user_followings do |t|
      t.references :user, null: false, foreign_key: true
      t.integer :following

      t.timestamps

      t.index %i[user_id following], unique: true
    end
  end
end
