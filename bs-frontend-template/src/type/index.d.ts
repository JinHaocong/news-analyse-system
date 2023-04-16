export { }
declare global {
    type echarts = any
    interface IResponse<T = any> {
        Code: number;
        Msg: string;
        Data: T;
    }
    interface IObject<T> {
        [index: string]: T
    }

    interface ITable<T = any> {
        data: Array<T>
        total: number
        page: number
        size: number
    }
    interface ImportMetaEnv {
        VITE_APP_TITLE: string
        VITE_PORT: number
        VITE_PROXY: string
        VITE_API_BASE_URL: string
        VITE_LOGIN_REQUIRED: string
    }
}