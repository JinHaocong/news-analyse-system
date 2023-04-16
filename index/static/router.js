const routes = [{
        path: '/table',
        component: TableView
    },
    {
        path: '/recommand',
        component: RecommandView
    },
    {
        path: '/predict',
        component: PredictView
    },
    {
        path: '/area',
        component: AreaView
    },
    {
        path: '/workyear',
        component: WorkyearView
    },
    {
        path: '/salary',
        component: SalaryView
    },
    {
        path: '/degree',
        component: DegreeView
    },
    {
        path: '/profile',
        component: ProfileView
    },
    {
        path: '/password',
        component: PasswordView
    },
]
var router = new VueRouter({
    routes
})