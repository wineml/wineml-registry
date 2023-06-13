import axios from "axios";

let token = null;

const setToken = (newToken) => {
  token = `Bearer ${newToken}`;
};

const get = async ({ route, params = {}, timeout = 0 } = {}) => {
  const config = {
    params: params,
    timeout: timeout,
    headers: {
      Authorization: token,
    },
  };
  const res = await axios
    .get(
      `${process.env.REACT_APP_WINEML_SERVICE_URL}${route}`,
      config,
    )
    .then(function (res) {
      return res;
    })
    .catch(function (error) {
      return error;
    });

  if (res instanceof Error) {
    console.error(res);
    throw res;
  }
  return res;
};

const post = async ({ route, params = {}, body = {} } = {}) => {
  const config = {
    params: params,
    headers: {
      'Content-Type': 'application/json',
      Authorization: token,
    },
  };
  const res = await axios
    .post(
      `${process.env.REACT_APP_WINEML_SERVICE_URL}${route}`,
      body,
      config
    )
    .then(function (res) {
      return res;
    })
    .catch(function (error) {
      return error;
    });

    if (res instanceof Error) {
      console.error(res);
      throw res;
    }
    return res;
};


const put = async ({ route, params = {}, body = {} } = {}) => {
  const config = {
    params: params,
    headers: {
      'Content-Type': 'application/json',
      Authorization: token,
    },
  };
  const res = await axios
    .put(
      `${process.env.REACT_APP_WINEML_SERVICE_URL}${route}`,
      body,
      config
    )
    .then(function (res) {
      return res;
    })
    .catch(function (error) {
      return error;
    });

    if (res instanceof Error) {
      console.error(res);
      throw res;
    }
    return res;
};

const serviceCaller = {
  setToken,
  get,
  post,
  put,
};

export default serviceCaller;
