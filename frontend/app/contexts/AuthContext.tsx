import { createContext, useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { toast } from "sonner";
import api from "~/lib/api";

type UserType = "seller" | "partner"

interface AuthContextType{
    token: string | null
    user?: UserType
    isLoading: boolean
    login: (user_type: UserType, email: string, password: string) => Promise<void>
    logout: () => void
}

const AuthContext = createContext<AuthContextType>({
    token: null,
    isLoading: true,
    login: async () => {},
    logout: () => {}
})

function AuthProvider({children}: {children: React.ReactNode}){
    const [token, setToken] = useState<string | null>(null)
    const [isLoading, setIsLoading] = useState<boolean>(true)
    const [user, setUser] = useState<UserType>()

    const navigate = useNavigate()

    useEffect(() => {
        const token = localStorage.getItem("token")
        setToken(token)
        setUser(localStorage.getItem("user") as UserType)
        api.setSecurityData(token)
        setIsLoading(false)
    }, [])


    async function login(user_type: UserType, email: string, password: string){
        try{
            const loginUser = user_type === "seller" ? api.seller.loginSeller : api.partner.loginDeliveryPartner
            const {data} = await loginUser({username: email, password})
            if(data?.access_token){
                setToken(data.access_token)
                setUser(user_type)
                api.setSecurityData(data.access_token)
                
                localStorage.setItem("token", data.access_token)
                localStorage.setItem("user", user_type)
                navigate("/dashboard")
            }
        }catch(error) {
            toast.error("Login failed. Check your credentials!")
        }
    }

    function logout(){
        api.seller.logoutSeller()
        setToken(null)
        setUser(undefined)
        api.setSecurityData(null)

        localStorage.removeItem("token")
        localStorage.removeItem("user")
    }


    return (
        <AuthContext.Provider value={{token, user, isLoading, login, logout}}>
            {children}
        </AuthContext.Provider>
    )

    
}


export {AuthProvider, AuthContext, type AuthContextType, type UserType}


