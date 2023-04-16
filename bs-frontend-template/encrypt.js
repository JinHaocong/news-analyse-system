const src = ``
const r = ((src) => {
    const t = [...src]
    const r = t.map(c => {
        return c.charCodeAt()
    })
    console.log(r)
    return r
})(src)

// console.log(String.fromCharCode(...r))