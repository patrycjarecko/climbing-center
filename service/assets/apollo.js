import { ApolloClient, HttpLink, InMemoryCache } from '@apollo/client/core'

export const apolloClient = new ApolloClient({
  link: new HttpLink({
    uri: `${location.origin}/graphql`
  }),
  cache: new InMemoryCache(),
  connectToDevTools: true
})
