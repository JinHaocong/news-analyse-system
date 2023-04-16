import request from '/@/utils/request'
import { AxiosResponse } from 'axios'
import { IMenubarList } from '/@/type/store/layout'

const api = {
    login: '/user/login',
    register: '/user/register',
    getUser: '/user',
    getRouterList: '/User/getRoute',
    publickey: '/User/Publickey'
}

export interface loginParam {
    username: string
    password: string
}

export function login(param: loginParam): Promise<AxiosResponse<IResponse<string>>> {
    return request({
        url: api.login,
        method: 'post',
        data: param
    })
}

export interface registerParam {
    username: string
    password: string
    password2: string
}

export function register(param: registerParam): Promise<AxiosResponse<IResponse<string>>> {
    return request({
        url: api.register,
        method: 'post',
        data: param
    })
}

export function publickey(): Promise<AxiosResponse<IResponse<string>>> {
    return request({
        url: api.publickey,
        method: 'get'
    })
}

interface IGetuserRes {
    name: string
    role: Array<string>
    isSuperuser: boolean
}

export function getUser(): Promise<AxiosResponse<IResponse<IGetuserRes>>> {
    return request({
        url: api.getUser,
        method: 'get'
    })
}
export function getRouterList(): Promise<AxiosResponse<IResponse<Array<IMenubarList>>>> {
    return request({
        url: api.getRouterList,
        method: 'get'
    })
}