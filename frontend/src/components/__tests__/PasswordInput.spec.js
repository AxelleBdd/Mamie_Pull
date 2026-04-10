import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import PasswordInput from '../PasswordInput.vue'

describe('PasswordInput', () => {
  it('renders input element with correct attributes', () => {
    const wrapper = mount(PasswordInput, {
      props: {
        modelValue: '',
        name: 'password',
        id: 'password-field',
        placeholder: 'Enter password',
      },
    })

    const input = wrapper.find('input')
    expect(input.attributes('name')).toBe('password')
    expect(input.attributes('id')).toBe('password-field')
    expect(input.attributes('placeholder')).toBe('Enter password')
    expect(input.attributes('required')).toBeDefined()
  })

  it('toggles password visibility when button is clicked', async () => {
    const wrapper = mount(PasswordInput, {
      props: {
        modelValue: 'secret123',
      },
    })

    const input = wrapper.find('input')
    const button = wrapper.find('button')

    expect(input.attributes('type')).toBe('password')

    await button.trigger('click')

    expect(input.attributes('type')).toBe('text')

    await button.trigger('click')

    expect(input.attributes('type')).toBe('password')
  })

  it('updates modelValue when input value changes', async () => {
    const wrapper = mount(PasswordInput, {
      props: {
        modelValue: '',
      },
    })

    const input = wrapper.find('input')
    await input.setValue('newPassword')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['newPassword'])
  })

  it('displays correct aria-label based on visibility state', async () => {
    const wrapper = mount(PasswordInput, {
      props: {
        modelValue: '',
      },
    })

    const button = wrapper.find('button')

    expect(button.attributes('aria-label')).toBe('Afficher le mot de passe')

    await button.trigger('click')

    expect(button.attributes('aria-label')).toBe('Masquer le mot de passe')
  })
})
