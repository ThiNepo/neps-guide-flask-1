const app = Vue.createApp({
  data() {
    return {
      posts: [],
      is_registering: false,
      page: 1,
      pages: 1,
      text: "",
      token: null,
      //user: null,
      login_error_message: "",
      username: "",
      password: "",
      email: "",
      //BASE_URL: "https://guide-flask.herokuapp.com",
      BASE_URL: "http://localhost:5000",
    };
  },
  mounted() {
    this.fetch_posts();
  },
  methods: {
    fetch_posts(page = 1) {
      if (this.token) {
        axios
          .get(`${this.BASE_URL}/posts/`, {
            headers: { Authorization: `Bearer ${this.token}` },
            params: { page: page, reversed: true },
          })
          .then((response) => {
            console.log(response);
            this.page = response.data.page;
            this.pages = response.data.pages;
            this.posts = response.data.posts;
          })
          .catch((error) => {
            console.log(error.response);
          });
      }
    },

    post() {
      if (this.text.length > 0) {
        axios
          .post(
            `${this.BASE_URL}/posts/`,
            {
              text: this.text,
            },
            { headers: { Authorization: `Bearer ${this.token}` } }
          )
          .then((response) => {
            this.text = "";
            this.fetch_posts();
          });
      }
    },

    login() {
      axios
        .post(`${this.BASE_URL}/auth/login`, {
          username: this.username,
          password: this.password,
        })
        .then((response) => {
          this.token = response.data.access_token;
          this.fetch_posts();
        })
        .catch((error) => {
          this.login_error_message = error.response.data.msg;
        });
    },

    register() {
      axios
        .post(`${this.BASE_URL}/users/`, {
          username: this.username,
          password: this.password,
          email: this.email,
        })
        .then((response) => {
          this.is_registering = false;
        })
        .catch((error) => {
          this.login_error_message = error.response.data.msg;
        });
    },
  },
  watch: {
    page() {
      this.fetch_posts(this.page);
    },
  },
});
