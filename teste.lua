-- Num args errado
function ok(x)
    return x
end

function main()
    local y = ok(2, 1)

    print(y)
end
main()