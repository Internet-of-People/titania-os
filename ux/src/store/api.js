import Vue from 'vue'
import VueResource from 'vue-resource'
import VueLocalStorage from 'vue-ls'

Vue.use(VueResource)
Vue.use(VueLocalStorage)
const local_store = Vue.ls


// Vue.http.options.root = 'http://localhost:3000'

export default {
  // get (url, request) {
  //   return Vue.http.get(url, request)
  //     .then((response) => Promise.resolve(response))
  //     .catch((error) => Promise.reject(error))
  // },
  post (url, request) {
    return Vue.http.post(url, request, {emulateJSON: true})
      .then((response) => Promise.resolve(response))
      .catch((error) => Promise.reject(error))
  },
  postWithSession (url, request) {
    var user = local_store.get('user')
    var session_key = local_store.get('session_key_'+user)
    request.session_key = session_key
    return Vue.http.post(url, request, {emulateJSON: true})
      .then((response) => Promise.resolve(response))
      .catch((error) => Promise.reject(error))
  },
  postWithSessionAndUpload (url, request) {
    return Vue.http.post(url, request,{
      emulateJSON: true,
      headers: {
          'Content-Type': 'multipart/form-data'
      }
   })
  }
  // ,
  // patch (url, request) {
  //   return Vue.http.patch(url, request)
  //     .then((response) => Promise.resolve(response))
  //     .catch((error) => Promise.reject(error))
  // },
  // delete (url, request) {
  //   return Vue.http.delete(url, request)
  //     .then((response) => Promise.resolve(response))
  //     .catch((error) => Promise.reject(error))
  // }
}
