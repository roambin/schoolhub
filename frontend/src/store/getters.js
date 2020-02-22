const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  name: state => state.user.name,
  role: state => state.user.role,
  user_info: state => state.user.user_info,
  permission_routes: state => state.permission.routes
}
export default getters
