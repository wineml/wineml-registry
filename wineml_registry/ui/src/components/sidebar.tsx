import React from 'react';
import {
  // useContext,
  useState,
} from 'react';
// import { AuthContext } from '../authContext';
import { useNavigate, useLocation } from 'react-router-dom';
import { createStyles, Navbar, Group, Code, getStylesRef, rem, Text } from '@mantine/core';
import {
  // IconFingerprint,
  IconGlassFull,
  // IconSettings,
  // IconLogout,
} from '@tabler/icons-react';


// theme
const useStyles = createStyles((theme) => ({
  navbar: {backgroundColor: "#63032e"},

  version: {
    backgroundColor: theme.fn.lighten("#63032e", 0.3),
    color: theme.white,
    fontWeight: 700,
  },

  header: {
    paddingBottom: theme.spacing.md,
    marginBottom: `calc(${theme.spacing.md} * 1.5)`,
    borderBottom: `${rem(1)} solid ${theme.fn.lighten( "#63032e", 0.2)}`,
  },

  footer: {
    paddingTop: theme.spacing.md,
    marginTop: theme.spacing.md,
    borderTop: `${rem(1)} solid ${theme.fn.lighten( "#63032e", 0.2)}`,
  },

  link: {
    ...theme.fn.focusStyles(),
    display: 'flex',
    alignItems: 'center',
    textDecoration: 'none',
    fontSize: theme.fontSizes.sm,
    color: theme.white,
    padding: `${theme.spacing.xs} ${theme.spacing.sm}`,
    borderRadius: theme.radius.sm,
    fontWeight: 500,

    '&:hover': {
      backgroundColor: theme.fn.lighten("#63032e", 0.2),
    },
  },

  logout: {
    ...theme.fn.focusStyles(),
    display: 'flex',
    alignItems: 'center',
    textDecoration: 'none',
    fontSize: theme.fontSizes.sm,
    color: theme.white,
    padding: `${theme.spacing.xs} ${theme.spacing.sm}`,
    borderRadius: theme.radius.sm,
    fontWeight: 500,
    backgroundColor: "#A40000",
  },

  linkIcon: {
    ref: getStylesRef('icon'),
    color: theme.white,
    opacity: 0.75,
    marginRight: theme.spacing.sm,
  },

  linkActive: {
    '&, &:hover': {
      backgroundColor: theme.fn.lighten("#63032e", 0.2),
      [`& .${getStylesRef('icon')}`]: {opacity: 0.9},
    },
  },
}));

const navbarItems = [
  { link: '/home', label: 'Models', icon: IconGlassFull },
  // { link: '/settings', label: 'Settings', icon: IconSettings },
];

export function SideBar() {
  const navigate = useNavigate();
  const location = useLocation();
  const { classes, cx } = useStyles();
  const [ active, setActive ] = useState(location.pathname);
  // const { logout } = useContext(AuthContext);

  function handleSidebarClick(event, route) {
    event.preventDefault();
    setActive(route);
    navigate(route);
  }

  // function handleLogout() {
  //   logout();
  //   window.location.reload();
  // }

  const links = navbarItems.map((item) => (
    <a
      className={cx(classes.link, { [classes.linkActive]: item.link === active })}
      href={item.link}
      key={item.link}
      onClick={(event) => {
        handleSidebarClick(event, item.link);
      }}
    >
      <item.icon className={classes.linkIcon} stroke={1.5} />
      <span>{item.label}</span>
    </a>
  ));

  return (
    <Navbar width={{ sm: 250 }} p="md" className={classes.navbar}>
      <Navbar.Section grow>
        <Group className={classes.header} position="apart">
          <Text fz="xl" ta="right" sx={(theme) => ({ fontFamily: `Greycliff CF, ${theme.fontFamily}`, fontWeight: 700 , color: "white"})}>WineML</Text>
          <Code className={classes.version}>v0.0.1</Code>
        </Group>
        {links}
      </Navbar.Section>

      {/* <Navbar.Section className={classes.footer}>
        <a href="/account" className={classes.link} onClick={(event) => {
            handleSidebarClick(event, "/account");
          }}
        >
          <IconFingerprint className={classes.linkIcon} stroke={1.5} />
          <span>Account</span>
        </a>
        <a href="/" className={classes.logout} onClick={handleLogout}>
          <IconLogout className={classes.linkIcon} stroke={1.5} />
          <span>Logout</span>
        </a>
      </Navbar.Section> */}
    </Navbar>
  );
}

export default SideBar;
