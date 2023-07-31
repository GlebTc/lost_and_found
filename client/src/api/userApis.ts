import axios, {AxiosResponse} from 'axios';

const baseURL = 'http://localhost:8000/api/v1';

interface userLogin {
    user_email: string;
    user_password: string;
}

export const userLogin = async (loginValues: userLogin): Promise<AxiosResponse> => {
    return await axios.post(`${baseURL}/login`, loginValues);
}