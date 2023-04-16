import { ComponentOptions } from 'vue'
export default <ComponentOptions>{
    data() {
        return {
            ImportMetaEnv: import.meta.env
        }
    },
    methods: {
        toPage(name: string): void {
            this.$router.push({ name })
        },
    }
}