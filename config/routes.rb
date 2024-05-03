Rails.application.routes.draw do
  root to: 'tweets#index'

  # devise_for :users
  devise_for :users,
             controllers: {
               omniauth_callbacks: 'users/omniauth_callbacks'
             }
  resources :users do
    resource :follow, only: %i[create destroy]
    resource :following, only: [:show]
    resource :followers, only: [:show]
  end
  get 'users/:id/likes', to: 'users#likes', as: 'user_likes'
  get 'settings', to: 'users#settings', as: 'settings'
  patch 'settings', to: 'users#settings_update'

  resources :tweets do
    resource :like, only: %i[create destroy show]
  end
  get 'page', to: 'tweets#page', as: 'page'

  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Reveal health status on /up that returns 200 if the app boots with no exceptions, otherwise 500.
  # Can be used by load balancers and uptime monitors to verify that the app is live.
  # get "up" => "rails/health#show", as: :rails_health_check

  # Defines the root path route ("/")
  # root "posts#index"
end
